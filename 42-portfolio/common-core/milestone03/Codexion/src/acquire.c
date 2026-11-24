/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   acquire.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:04:38 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_time	pair_available(t_coder *coder)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &coder->sim->dongles[coder->left];
	right = &coder->sim->dongles[coder->right];
	if (left->heap[0] != coder || right->heap[0] != coder)
		return (PAIR_WAIT);
	if (left->owner != 0 || right->owner != 0)
		return (PAIR_WAIT);
	if (left->ready_at > right->ready_at)
		return (left->ready_at);
	return (right->ready_at);
}

static void	grant_pair(t_coder *coder, t_time at)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &coder->sim->dongles[coder->left];
	right = &coder->sim->dongles[coder->right];
	heap_remove(left);
	heap_remove(right);
	left->owner = coder->id;
	right->owner = coder->id;
	coder->queued = 0;
	coder->last_start = at;
	coder->state = CODER_COMPILING;
}

static t_time	attempt_pair(t_coder *coder)
{
	t_time	ready;
	t_time	at;

	if (!pair_lock_validated(coder))
		return (PAIR_ERROR);
	if (!pair_requested(coder))
	{
		sim_error(coder->sim, "grant: invalid pair request", coder->id);
		pair_unlock(coder);
		return (PAIR_ERROR);
	}
	ready = pair_available(coder);
	at = now_us(coder->sim);
	if (ready >= 0 && ready <= at
		&& expired_coder(coder->sim, at) == -1)
	{
		grant_pair(coder, at);
		ready = PAIR_GRANTED;
	}
	if (!pair_unlock(coder))
		return (PAIR_ERROR);
	return (ready);
}

int	acquire_pair(t_coder *coder)
{
	t_time	result;

	if (!coder_state_valid(coder) || !coder->queued
		|| coder->left == coder->right)
		return (coder_error(coder, "acquire: invalid pair request", EINVAL));
	while (sim_live(coder->sim))
	{
		result = attempt_pair(coder);
		if (result == PAIR_GRANTED)
		{
			log_compile(coder, coder->last_start);
			sim_notify(coder->sim, 0);
			sim_notify(coder->sim, 1);
			return (1);
		}
		if (result == PAIR_ERROR)
			return (0);
		if (result < 0)
			wait_event(coder->sim);
		else
			wait_until(coder->sim, &coder->sim->event, result);
	}
	return (0);
}

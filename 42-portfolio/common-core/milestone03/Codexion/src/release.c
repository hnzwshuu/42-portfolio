/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   release.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:10 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	unown_pair(t_coder *coder)
{
	t_dongle	*left;
	t_dongle	*right;
	t_time		ready;

	left = &coder->sim->dongles[coder->left];
	right = &coder->sim->dongles[coder->right];
	if (!pair_valid(coder) || coder->queued
		|| left->owner != coder->id || right->owner != coder->id)
		return (coder_error(coder, "release: ownership mismatch", coder->id));
	left->owner = 0;
	right->owner = 0;
	coder->released_at = now_us(coder->sim);
	ready = deadline_after(coder->sim, coder->released_at,
			coder->sim->conf.cooldown);
	if (ready < 0)
		return (0);
	left->ready_at = ready;
	right->ready_at = ready;
	return (1);
}

int	release_pair(t_coder *coder)
{
	int	result;

	if (!coder_state_valid(coder))
		return (coder_error(coder, "release: invalid coder/index", EINVAL));
	if (!pair_lock_validated(coder))
		return (0);
	result = unown_pair(coder);
	if (!pair_unlock(coder))
		return (0);
	if (result)
		result = sim_notify(coder->sim, 0);
	return (result);
}

void	single_coder(t_coder *coder)
{
	if (!coder_state_valid(coder) || coder->sim->capacity != 1)
	{
		coder_error(coder, "single coder: invalid context", EINVAL);
		return ;
	}
	if (!pair_lock_validated(coder))
		return ;
	if (!pair_valid(coder) || coder->sim->dongles[0].owner != 0)
	{
		sim_error(coder->sim, "single coder: dongle already owned", coder->id);
		pair_unlock(coder);
		return ;
	}
	coder->sim->dongles[coder->left].owner = coder->id;
	coder->state = CODER_SINGLE;
	pair_unlock(coder);
	log_state(coder, "has taken a dongle", now_us(coder->sim));
	while (sim_live(coder->sim))
		wait_event(coder->sim);
	release_pair(coder);
}

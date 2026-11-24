/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:08 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	can_queue(t_coder *coder)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &coder->sim->dongles[coder->left];
	right = &coder->sim->dongles[coder->right];
	if (coder->state != CODER_WAITING && coder->state != CODER_REFACTORING)
		return (sim_error(coder->sim, "request: invalid phase", coder->id));
	if (!pair_valid(coder) || coder->queued || coder->left == coder->right)
		return (coder_error(coder,
				"request: invalid/duplicate state", coder->id));
	if (left->owner == coder->id || right->owner == coder->id)
		return (coder_error(coder, "request: already owns dongle", coder->id));
	if (!heap_accepts(left, coder) || !heap_accepts(right, coder))
		return (coder_error(coder, "request: invalid/full queue", coder->id));
	if (coder->sim->next_ticket == ULLONG_MAX)
		return (sim_error(coder->sim, "request: ticket overflow", ERANGE));
	return (1);
}

static void	enqueue_pair(t_coder *coder)
{
	coder->ticket = coder->sim->next_ticket++;
	heap_insert(&coder->sim->dongles[coder->left], coder);
	heap_insert(&coder->sim->dongles[coder->right], coder);
	coder->queued = 1;
}

int	queue_request(t_coder *coder)
{
	int	result;

	if (!coder_state_valid(coder))
		return (coder_error(coder, "request: invalid coder/index", EINVAL));
	if (!pair_lock_validated(coder))
		return (0);
	result = can_queue(coder);
	if (result)
		enqueue_pair(coder);
	if (!pair_unlock(coder))
		return (0);
	if (result)
		result = sim_notify(coder->sim, 0);
	return (result);
}

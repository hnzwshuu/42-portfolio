/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pair_validate.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:04 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	dongle_valid(t_sim *sim, int index)
{
	t_dongle	*dongle;
	t_coder		*entry;
	int			neighbor;
	int			i;

	dongle = &sim->dongles[index];
	neighbor = index;
	if (index == 0)
		neighbor = sim->capacity;
	if (!heap_valid(dongle) || dongle->ready_at < 0
		|| (dongle->owner != 0 && dongle->owner != index + 1
			&& dongle->owner != neighbor))
		return (0);
	i = 0;
	while (i < dongle->size)
	{
		entry = dongle->heap[i++];
		if (!coder_state_valid(entry) || entry->sim != sim || !entry->queued
			|| (entry->left != index && entry->right != index))
			return (0);
	}
	return (1);
}

int	pair_valid(t_coder *coder)
{
	return (dongle_valid(coder->sim, coder->left)
		&& (coder->left == coder->right
			|| dongle_valid(coder->sim, coder->right)));
}

static int	heap_contains(t_dongle *dongle, t_coder *coder)
{
	int	index;

	index = 0;
	while (index < dongle->size)
	{
		if (dongle->heap[index++] == coder)
			return (1);
	}
	return (0);
}

int	pair_requested(t_coder *coder)
{
	if (!pair_valid(coder) || !coder->queued || coder->left == coder->right)
		return (0);
	return (heap_contains(&coder->sim->dongles[coder->left], coder)
		&& heap_contains(&coder->sim->dongles[coder->right], coder));
}

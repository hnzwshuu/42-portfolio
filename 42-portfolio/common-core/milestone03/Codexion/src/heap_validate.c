/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_validate.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:36 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	request_valid(t_coder *coder)
{
	return (coder && coder->sim
		&& (coder->sim->conf.edf == 0 || coder->sim->conf.edf == 1)
		&& coder->id >= 1 && coder->id <= coder->sim->conf.count
		&& coder->last_start >= 0);
}

static int	heap_pair_valid(t_dongle *dongle)
{
	if (dongle->size != HEAP_CAPACITY)
		return (1);
	if (dongle->heap[0] == dongle->heap[1]
		|| dongle->heap[0]->id == dongle->heap[1]->id
		|| dongle->heap[0]->sim != dongle->heap[1]->sim)
		return (0);
	return (!request_order(dongle->heap[1], dongle->heap[0]));
}

int	heap_valid(t_dongle *dongle)
{
	int	index;

	if (!dongle || dongle->size < 0 || dongle->size > HEAP_CAPACITY)
		return (0);
	index = 0;
	while (index < HEAP_CAPACITY)
	{
		if (index < dongle->size && !request_valid(dongle->heap[index]))
			return (0);
		if (index >= dongle->size && dongle->heap[index] != NULL)
			return (0);
		index++;
	}
	return (heap_pair_valid(dongle));
}

int	heap_can_push(t_dongle *dongle, t_coder *coder)
{
	if (!heap_valid(dongle) || !request_valid(coder))
		return (0);
	return (heap_accepts(dongle, coder));
}

int	heap_accepts(t_dongle *dongle, t_coder *coder)
{
	int	index;

	if (dongle->size == HEAP_CAPACITY)
		return (0);
	if (dongle->size > 0 && dongle->heap[0]->sim != coder->sim)
		return (0);
	index = 0;
	while (index < dongle->size)
	{
		if (dongle->heap[index] == coder
			|| dongle->heap[index]->id == coder->id)
			return (0);
		index++;
	}
	return (1);
}

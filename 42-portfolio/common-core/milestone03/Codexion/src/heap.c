/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:39 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	request_order(t_coder *a, t_coder *b)
{
	if (a->sim->conf.edf && a->last_start != b->last_start)
		return (a->last_start < b->last_start);
	if (a->ticket != b->ticket)
		return (a->ticket < b->ticket);
	return (a->id < b->id);
}

int	request_before(t_coder *a, t_coder *b)
{
	if (!request_valid(a) || !request_valid(b))
		return (boundary_error("heap comparison: invalid request", -1));
	if (a->sim != b->sim)
		return (boundary_error("heap comparison: different simulations",
				a->id));
	return (request_order(a, b));
}

int	heap_push(t_dongle *dongle, t_coder *coder)
{
	if (!dongle)
		return (boundary_error("heap push: null dongle", -1));
	if (!heap_can_push(dongle, coder))
		return (boundary_error("heap push: invalid/full/duplicate request",
				dongle->size));
	heap_insert(dongle, coder);
	return (1);
}

t_coder	*heap_pop(t_dongle *dongle)
{
	int	size;

	size = -1;
	if (dongle)
		size = dongle->size;
	if (!heap_valid(dongle))
	{
		boundary_error("heap pop: invalid state", size);
		return (NULL);
	}
	if (size == 0)
		return (NULL);
	return (heap_remove(dongle));
}

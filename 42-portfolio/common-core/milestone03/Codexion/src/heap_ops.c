/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_ops.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:34 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	heap_swap(t_dongle *dongle, int first, int second)
{
	t_coder	*temp;

	temp = dongle->heap[first];
	dongle->heap[first] = dongle->heap[second];
	dongle->heap[second] = temp;
}

void	heap_insert(t_dongle *dongle, t_coder *coder)
{
	int	index;
	int	parent;

	index = dongle->size;
	dongle->heap[index] = coder;
	dongle->size++;
	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!request_order(dongle->heap[index], dongle->heap[parent]))
			break ;
		heap_swap(dongle, index, parent);
		index = parent;
	}
}

static void	heap_down(t_dongle *dongle)
{
	int	index;
	int	child;

	index = 0;
	while (index * 2 + 1 < dongle->size)
	{
		child = index * 2 + 1;
		if (child + 1 < dongle->size && request_order(
				dongle->heap[child + 1], dongle->heap[child]))
			child++;
		if (!request_order(dongle->heap[child], dongle->heap[index]))
			break ;
		heap_swap(dongle, index, child);
		index = child;
	}
}

t_coder	*heap_remove(t_dongle *dongle)
{
	t_coder	*result;

	result = dongle->heap[0];
	dongle->size--;
	dongle->heap[0] = dongle->heap[dongle->size];
	dongle->heap[dongle->size] = NULL;
	heap_down(dongle);
	return (result);
}

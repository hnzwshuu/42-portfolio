/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_medium_01.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 16:17:11 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/27 17:33:31 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

size_t	int_sqrt(size_t size)
{
	size_t	i;

	i = 1;
	while (size > i * i)
		i++;
	return (i);
}

size_t	value_rank(t_stack **stack, long value)
{
	size_t	rank;
	t_stack	*tmp;

	rank = 0;
	tmp = *(stack + A);
	while (tmp)
	{
		if (value > tmp->content)
			rank++;
		tmp = tmp->next;
	}
	tmp = *(stack + B);
	while (tmp)
	{
		if (value > tmp->content)
			rank++;
		tmp = tmp->next;
	}
	return (rank);
}

void	push_chunks_to_b(t_stack **stack, int *counter)
{
	size_t	rank;
	size_t	size;
	size_t	chunk;
	size_t	pushed;

	pushed = 0;
	size = stack_size(*(stack + A));
	chunk = int_sqrt(size);
	while (*(stack + A))
	{
		rank = value_rank(stack, (*(stack + A))->content);
		if (rank <= pushed)
		{
			operations(stack, "pb", counter);
			operations(stack, "rb", counter);
			pushed++;
		}
		else if (rank < pushed + chunk)
		{
			operations(stack, "pb", counter);
			pushed++;
		}
		else
			operations(stack, "ra", counter);
	}
}

void	move_mex_to_a(t_stack **stack, int *counter)
{
	size_t	size;
	size_t	pos;

	pos = max_position(*(stack + B));
	size = stack_size(*(stack + B));
	if (pos <= size / 2)
	{
		while (pos > 0)
		{
			pos--;
			operations(stack, "rb", counter);
		}
	}
	else
	{
		while (pos < size)
		{
			pos++;
			operations(stack, "rrb", counter);
		}
	}
	operations(stack, "pa", counter);
}

void	sort_medium(t_stack **stack, int *counter)
{
	if (is_sorted(stack) == 1)
		return ;
	if (*(stack + A))
		push_chunks_to_b(stack, counter);
	while (*(stack + B))
		move_mex_to_a(stack, counter);
	return ;
}

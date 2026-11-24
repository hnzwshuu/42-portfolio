/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_simple.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 16:17:06 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/27 17:33:17 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack **stack)
{
	t_stack	*tmp;

	tmp = *(stack + A);
	while (tmp->next)
	{
		if (tmp->content > tmp->next->content)
			return (0);
		tmp = tmp->next;
	}
	return (1);
}

size_t	stack_size(t_stack *stack)
{
	size_t	size;

	size = 0;
	while (stack)
	{
		size++;
		stack = stack->next;
	}
	return (size);
}

size_t	min_position(t_stack **stack)
{
	long	min_value;
	size_t	min_position;
	size_t	i;
	t_stack	*tmp;

	tmp = *(stack + A);
	min_value = tmp->content;
	min_position = 0;
	i = 0;
	while (tmp)
	{
		if (min_value > tmp->content)
		{
			min_value = tmp->content;
			min_position = i;
		}
		tmp = tmp->next;
		i++;
	}
	return (min_position);
}

void	move_min_to_top(t_stack **stack, int *counter)
{
	size_t	position;
	size_t	size;

	position = min_position(stack);
	size = stack_size(*(stack + A));
	if (size == 1)
		return ;
	if (position <= size / 2)
	{
		while (position > 0)
		{
			position--;
			operations(stack, "ra", counter);
		}
	}
	else
	{
		while (position < size)
		{
			position++;
			operations(stack, "rra", counter);
		}
	}
}

void	sort_simple(t_stack **stack, int *counter)
{
	if (is_sorted(stack) == 1)
		return ;
	while (*(stack + A))
	{
		move_min_to_top(stack, counter);
		operations(stack, "pb", counter);
	}
	while (*(stack + B))
		operations(stack, "pa", counter);
	return ;
}

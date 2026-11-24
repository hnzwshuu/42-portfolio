/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_mini.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 19:19:45 by soarai            #+#    #+#             */
/*   Updated: 2026/05/28 10:34:54 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_under_three(t_stack **stack, int *counter)
{
	t_stack	*second;

	second = (*(stack + A))->next;
	if ((*(stack + A))->content > second->content)
		operations(stack, "sa", counter);
	if (is_sorted(stack))
		return ;
	operations(stack, "rra", counter);
	second = (*(stack + A))->next;
	if ((*(stack + A))->content > second->content)
		operations(stack, "sa", counter);
	return ;
}

void	sort_under_five(t_stack **stack, int *counter)
{
	size_t	size;

	size = ft_lstsize(*(stack + A));
	if (size == 5)
	{
		move_min_to_top(stack, counter);
		operations(stack, "pb", counter);
	}
	move_min_to_top(stack, counter);
	operations(stack, "pb", counter);
	sort_under_three(stack, counter);
	while (*(stack + B) != NULL)
		operations(stack, "pa", counter);
	return ;
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_complex_01.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 13:47:50 by soarai            #+#    #+#             */
/*   Updated: 2026/05/28 11:01:28 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

long	max_rank(t_stack **stack)
{
	long	max_digit;
	long	rank;
	t_stack	*tmp;

	max_digit = 0;
	rank = 0;
	tmp = *(stack + A);
	while (tmp)
	{
		rank = value_rank(stack, tmp->content);
		if (rank > max_digit)
			max_digit = rank;
		tmp = tmp->next;
	}
	return (max_digit);
}

void	sort_complex(t_stack **stack, int *counter)
{
	long	max_rank_value;
	long	place;

	max_rank_value = max_rank(stack);
	place = 0;
	while (1)
	{
		sort_place(stack, place++, counter);
		while (*(stack + B) != NULL)
			operations(stack, "pa", counter);
		if (max_rank_value == 0)
			break ;
		max_rank_value /= 2;
	}
	return ;
}

void	sort_place(t_stack **stack, size_t place, int *counter)
{
	size_t	size;
	size_t	i;

	place = make_place(place);
	size = ft_lstsize(*(stack + A));
	i = 0;
	while (i < size)
	{
		if (match_target(value_rank(stack, (*(stack + A))->content), place, 0))
			operations(stack, "pb", counter);
		else
			operations(stack, "ra", counter);
		i++;
	}
	return ;
}

bool	match_target(size_t rank, size_t place, int target)
{
	long		num_place;

	num_place = ((rank / place) % 2);
	if (num_place == target)
		return (true);
	return (false);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium_02.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 15:18:45 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 15:18:57 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

size_t	max_position(t_stack *stack)
{
	long	max;
	size_t	pos;
	size_t	i;

	max = stack->content;
	pos = 0;
	i = 0;
	while (stack)
	{
		if (max < stack->content)
		{
			max = stack->content;
			pos = i;
		}
		stack = stack->next;
		i++;
	}
	return (pos);
}

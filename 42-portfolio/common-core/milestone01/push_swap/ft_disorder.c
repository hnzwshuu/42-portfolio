/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   disorder.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 12:52:00 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 15:13:53 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

long	measure_disorder(t_stack **stack)
{
	long	mistakes;
	long	total;
	t_stack	*i;
	t_stack	*j;

	mistakes = 0;
	total = 0;
	i = *(stack + A);
	while (i != NULL)
	{
		j = i->next;
		while (j != NULL)
		{
			if (i->content > j->content)
				mistakes++;
			total++;
			j = j->next;
		}
		i = i->next;
	}
	if (mistakes == 0)
		return (0);
	return (mistakes * 10000 / total);
}

void	init_operation_counter(int *counter)
{
	int	i;

	i = 0;
	while (i < 11)
	{
		counter[i] = 0;
		i++;
	}
	return ;
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 16:17:21 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/26 16:21:00 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	pa(t_stack **stack)
{
	t_stack	*tmp_a_first;
	t_stack	*tmp_b_second;

	if ((*(stack + B)) == NULL)
		return ;
	tmp_a_first = *(stack + A);
	tmp_b_second = (*(stack + B))->next;
	*(stack + A) = *(stack + B);
	(*(stack + B))->next = tmp_a_first;
	*(stack + B) = tmp_b_second;
}

void	pb(t_stack **stack)
{
	t_stack	*tmp_a_second;
	t_stack	*tmp_b_first;

	if ((*(stack + A)) == NULL)
		return ;
	tmp_b_first = *(stack + B);
	tmp_a_second = (*(stack + A))->next;
	*(stack + B) = *(stack + A);
	(*(stack + A))->next = tmp_b_first;
	*(stack + A) = tmp_a_second;
}

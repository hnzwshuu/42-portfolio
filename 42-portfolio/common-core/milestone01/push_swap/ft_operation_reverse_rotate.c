/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operation_reverse_rotate.c                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 16:17:18 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/27 16:03:44 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*lstbeforelast(t_stack **stack, size_t sp)
{
	t_stack	*before_last;

	while ((*(stack + sp))->next->next)
		*(stack + sp) = (*(stack + sp))->next;
	before_last = *(stack + sp);
	return (before_last);
}

void	rra(t_stack **stack)
{
	t_stack	*tmp_first;
	t_stack	*before_last;
	t_stack	*last;

	if (*(stack + A) == NULL || (*(stack + A))->next == NULL)
		return ;
	tmp_first = *(stack + A);
	before_last = lstbeforelast(stack, A);
	last = before_last->next;
	last->next = tmp_first;
	(*(stack + A)) = last;
	before_last->next = NULL;
}

void	rrb(t_stack **stack)
{
	t_stack	*tmp_first;
	t_stack	*before_last;
	t_stack	*last;

	if (*(stack + B) == NULL || (*(stack + B))->next == NULL)
		return ;
	tmp_first = *(stack + B);
	before_last = lstbeforelast(stack, B);
	last = before_last->next;
	last->next = tmp_first;
	(*(stack + B)) = last;
	before_last->next = NULL;
}

void	rrr(t_stack **stack)
{
	rra(stack);
	rrb(stack);
}

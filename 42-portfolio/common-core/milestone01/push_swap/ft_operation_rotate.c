/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operation_rotate.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 16:17:15 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/27 16:04:55 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*lstlast(t_stack **stack, size_t sp)
{
	t_stack	*last;

	while ((*(stack + sp))->next)
		*(stack + sp) = (*(stack + sp))->next;
	last = *(stack + sp);
	return (last);
}

void	ra(t_stack **stack)
{
	t_stack	*tmp_first;
	t_stack	*tmp_second;
	t_stack	*last;

	if (*(stack + A) == NULL || (*(stack + A))->next == NULL)
		return ;
	tmp_first = *(stack + A);
	tmp_second = (*(stack + A))->next;
	last = lstlast(stack, A);
	last->next = tmp_first;
	tmp_first->next = NULL;
	(*(stack + A)) = tmp_second;
}

void	rb(t_stack **stack)
{
	t_stack	*tmp_first;
	t_stack	*tmp_second;
	t_stack	*last;

	if (*(stack + B) == NULL || (*(stack + B))->next == NULL)
		return ;
	tmp_first = *(stack + B);
	tmp_second = (*(stack + B))->next;
	last = lstlast(stack, B);
	last->next = tmp_first;
	tmp_first->next = NULL;
	(*(stack + B)) = tmp_second;
}

void	rr(t_stack **stack)
{
	ra(stack);
	rb(stack);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 16:16:58 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/26 16:16:59 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sa(t_stack **stack)
{
	t_stack	*tmp_first;
	t_stack	*tmp_third;

	if ((*(stack + A)) == NULL || (*(stack + A))->next == NULL)
		return ;
	tmp_first = *(stack + A);
	tmp_third = (*(stack + A))->next->next;
	*(stack + A) = (*(stack + A))->next;
	(*(stack + A))->next = tmp_first;
	(*(stack + A))->next->next = tmp_third;
}

void	sb(t_stack **stack)
{
	t_stack	*tmp_first;
	t_stack	*tmp_third;

	if ((*(stack + B)) == NULL || (*(stack + B))->next == NULL)
		return ;
	tmp_first = *(stack + B);
	tmp_third = (*(stack + B))->next->next;
	*(stack + B) = (*(stack + B))->next;
	(*(stack + B))->next = tmp_first;
	(*(stack + B))->next->next = tmp_third;
}

void	ss(t_stack **stack)
{
	sa(stack);
	sb(stack);
}

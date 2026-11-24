/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_stacklst.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 13:30:01 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 14:36:18 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*ft_lstnew(long content)
{
	t_stack	*node;

	node = (t_stack *)malloc(sizeof(t_stack));
	if (node == NULL)
		return (NULL);
	node->next = NULL;
	node->content = content;
	return (node);
}

void	ft_lstadd_front(t_stack **lst, t_stack *new, size_t sp)
{
	if (lst == NULL || new == NULL)
		return ;
	new->next = *(lst + sp);
	*(lst + sp) = new;
	return ;
}

void	ft_lstadd_back(t_stack **lst, t_stack *new, size_t sp)
{
	t_stack	*tmp;

	tmp = NULL;
	if (lst == NULL || new == NULL)
		return ;
	tmp = *(lst + sp);
	if (tmp == NULL)
	{
		*(lst + sp) = new;
		return ;
	}
	while (tmp->next != NULL)
		tmp = tmp->next;
	tmp->next = new;
	return ;
}

t_stack	**ft_lstclear(t_stack **lst, size_t sp)
{
	t_stack	*tmp;

	if (lst == NULL)
		return (NULL);
	while (*(lst + sp) != NULL)
	{
		tmp = (*(lst + sp))->next;
		free(*(lst + sp));
		*(lst + sp) = tmp;
	}
	*(lst + sp) = NULL;
	return (NULL);
}

int	ft_lstsize(t_stack *stack)
{
	size_t	count;

	count = 0;
	while (stack != NULL)
	{
		stack = stack->next;
		count++;
	}
	return (count);
}

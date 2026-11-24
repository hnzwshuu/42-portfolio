/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operations.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 13:59:49 by soarai            #+#    #+#             */
/*   Updated: 2026/05/26 13:39:46 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	operations(t_stack **stack, char *operation, int *counter)
{
	size_t	size;

	if (*operation == 's')
		operations_s(stack, operation, counter);
	else if (*operation == 'p')
		operations_p(stack, operation, counter);
	else if (*operation == 'r' && *(operation + 2) == '\0')
		operations_r(stack, operation, counter);
	else if (*operation == 'r' && *(operation + 2) != '\0')
		operations_rr(stack, operation, counter);
	else
		return ;
	size = ft_strlen(operation);
	write(1, operation, size);
	write(1, "\n", 1);
	return ;
}

void	operations_s(t_stack **stack, char *operation, int *counter)
{
	operation++;
	if (*operation == 'a')
	{
		sa(stack);
		(*(counter + SA))++;
	}
	else if (*operation == 'b')
	{
		sb(stack);
		(*(counter + SB))++;
	}
	else if (*operation == 's')
	{
		ss(stack);
		(*(counter + SS))++;
	}
	return ;
}

void	operations_p(t_stack **stack, char *operation, int *counter)
{
	operation++;
	if (*operation == 'a')
	{
		pa(stack);
		(*(counter + PA))++;
	}
	else if (*operation == 'b')
	{
		pb(stack);
		(*(counter + PB))++;
	}
	return ;
}

void	operations_r(t_stack **stack, char *operation, int *counter)
{
	operation++;
	if (*operation == 'a')
	{
		ra(stack);
		(*(counter + RA))++;
	}
	else if (*operation == 'b')
	{
		rb(stack);
		(*(counter + RB))++;
	}
	else if (*operation == 'r')
	{
		rr(stack);
		(*(counter + RR))++;
	}
	return ;
}

void	operations_rr(t_stack **stack, char *operation, int *counter)
{
	operation += 2;
	if (*operation == 'a')
	{
		rra(stack);
		(*(counter + RRA))++;
	}
	else if (*operation == 'b')
	{
		rrb(stack);
		(*(counter + RRB))++;
	}
	else if (*operation == 'r')
	{
		rrr(stack);
		(*(counter + RRR))++;
	}
	return ;
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bench.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 17:02:16 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 17:47:30 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	print_disorder(long disorder)
{
	long	top;
	long	last;

	write(2, "[bench] disorder:  ", 19);
	last = disorder % 100;
	top = disorder / 100;
	if (top < 10)
	{
		write(2, "0", 1);
		ft_putnbr_fd(top, 2);
	}
	else
		ft_putnbr_fd(top, 2);
	write(2, ".", 1);
	if (last < 10)
	{
		write(2, "0", 1);
		ft_putnbr_fd(last, 2);
	}
	else
		ft_putnbr_fd(last, 2);
	write(2, "%\n", 2);
	return ;
}

void	print_strategy(ssize_t strategy, long disorder)
{
	write(2, "[bench] strategy:  ", 19);
	if (strategy % 4 == 0)
		ft_putendl_fd("Simple / O(n^2)", 2);
	else if (strategy % 4 == 1)
		ft_putendl_fd("Medium / O(n√n)", 2);
	else if (strategy % 4 == 2)
		ft_putendl_fd("Complex / O(n log n)", 2);
	else if (strategy % 4 == 3)
	{
		if (disorder < 2000)
			ft_putendl_fd("Adaptive / O(n^2)", 2);
		else if (disorder >= 2000 && disorder < 5000)
			ft_putendl_fd("Adaptive / O(n√n)", 2);
		else if (disorder >= 5000)
			ft_putendl_fd("Adaptive / O(n log n)", 2);
	}
	return ;
}

void	print_counter(int *counter)
{
	long	sum;
	int		i;

	i = 0;
	sum = 0;
	while (i < 11)
	{
		sum += counter[i];
		i++;
	}
	write(2, "[bench] total_ops:  ", 20);
	ft_putnbr_fd(sum, 2);
	write(2, "\n", 1);
	i = 0;
	while (i < 11)
	{
		print_counter_elements(counter, i);
		i++;
	}
	return ;
}

void	print_counter_elements(int *counter, int element)
{
	if (element == SA || element == RA)
		write(2, "[bench] ", 8);
	else
		write(2, "  ", 2);
	print_operations(element);
	write(2, ":  ", 3);
	ft_putnbr_fd(counter[element], 2);
	if (element == PB || element == RRR)
		write(2, "\n", 1);
	return ;
}

void	print_operations(int element)
{
	if (element == SA)
		write(2, "sa", 2);
	else if (element == SB)
		write(2, "sb", 2);
	else if (element == SS)
		write(2, "ss", 2);
	else if (element == PA)
		write(2, "pa", 2);
	else if (element == PB)
		write(2, "pb", 2);
	else if (element == RA)
		write(2, "ra", 2);
	else if (element == RB)
		write(2, "rb", 2);
	else if (element == RR)
		write(2, "rr", 2);
	else if (element == RRA)
		write(2, "rra", 3);
	else if (element == RRB)
		write(2, "rrb", 3);
	else if (element == RRR)
		write(2, "rrr", 3);
	return ;
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/15 16:22:15 by soarai            #+#    #+#             */
/*   Updated: 2026/05/28 14:03:32 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack	**stack;
	ssize_t	strategy;
	int		counter[11];

	stack = malloc_dps();
	strategy = 0;
	if (argc >= 2 && argv != NULL && stack != NULL)
		strategy = solve_cmdline(argv, stack);
	if (strategy == ERROR || stack == NULL)
	{
		write(2, "Error\n", 6);
		return (ERROR);
	}
	init_operation_counter(counter);
	solve_sort(stack, strategy, counter);
	ft_lstclear(stack, A);
	ft_lstclear(stack, B);
	free(stack);
	return (0);
}

ssize_t	solve_cmdline(char **argv, t_stack **stack)
{
	ssize_t	option;

	option = define_option(argv);
	if (option == ERROR)
	{
		free(stack);
		return (ERROR);
	}
	if (option >= 4)
		argv++;
	if (malloc_stack(argv, stack) == NULL)
		return (ERROR);
	return (option);
}

void	solve_sort(t_stack **stack, ssize_t strategy, int *counter)
{
	size_t	bench;
	long	disorder;

	bench = 0;
	if (strategy >= 4)
		bench = BENCH;
	disorder = measure_disorder(stack);
	if (disorder == 0)
	{
		if (bench == BENCH)
			solve_benchmark(strategy, disorder, counter);
		return ;
	}
	if (ft_lstsize(*(stack + A)) <= 5)
		solve_stack_mini(stack, counter);
	else if (strategy == 0 || strategy % 4 == 0)
		sort_simple(stack, counter);
	else if (strategy % 4 == 1)
		sort_medium(stack, counter);
	else if (strategy % 4 == 2)
		sort_complex(stack, counter);
	else if (strategy % 4 == 3)
		sort_adaptive(stack, counter, disorder);
	if (bench == BENCH)
		solve_benchmark(strategy, disorder, counter);
}

void	solve_benchmark(ssize_t strategy, long disorder, int *counter)
{
	print_disorder(disorder);
	print_strategy(strategy, disorder);
	print_counter(counter);
	return ;
}

void	solve_stack_mini(t_stack **stack, int *counter)
{
	if (ft_lstsize(*(stack + A)) <= 3)
		sort_under_three(stack, counter);
	else
		sort_under_five(stack, counter);
	return ;
}

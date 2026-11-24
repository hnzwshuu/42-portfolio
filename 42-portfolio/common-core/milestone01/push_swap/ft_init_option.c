/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_init_option.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 12:55:17 by soarai            #+#    #+#             */
/*   Updated: 2026/05/28 10:57:41 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

ssize_t	define_option(char **argv)
{
	ssize_t	bench;
	ssize_t	strategy;

	bench = 0;
	argv++;
	if (hyphen_or_digit(*argv) == 0 && *(*argv + 2) == 'b')
	{
		bench = match_strategy((*argv + 2), "bench", BENCH);
		argv++;
	}
	if (bench == ERROR)
		return (ERROR);
	strategy = define_strategy(*argv);
	if (strategy == ERROR)
		return (ERROR);
	return (bench + strategy);
}

ssize_t	define_strategy(char *strategy)
{
	ssize_t	value;

	if (strategy == NULL)
		return (ERROR);
	value = hyphen_or_digit(strategy);
	if (value == ERROR)
		return (ERROR);
	else if (value == ADAPTIVE)
		return (ADAPTIVE);
	strategy += 2;
	if (*strategy == 's')
		return (match_strategy(strategy, "simple", SIMPLE));
	else if (*strategy == 'm')
		return (match_strategy(strategy, "medium", MEDIUM));
	else if (*strategy == 'c')
		return (match_strategy(strategy, "complex", COMPLEX));
	else if (*strategy == 'a')
		return (match_strategy(strategy, "adaptive", ADAPTIVE));
	else
		return (ERROR);
}

ssize_t	match_strategy(char *strategy, char *target, ssize_t value)
{
	size_t	i;

	i = 0;
	while (*(target + i) != '\0')
	{
		if (*(strategy + i) != *(target + i))
			return (ERROR);
		i++;
	}
	if (*(strategy + i) != '\0')
		return (ERROR);
	return (value);
}

ssize_t	hyphen_or_digit(char *strategy)
{
	if (*strategy == '-')
	{
		if (*(strategy + 1) == '-')
			return (0);
		else if (*(strategy + 1) >= '0' && *(strategy + 1) <= '9')
			return (ADAPTIVE);
	}
	else if (*strategy == '+' || (*strategy >= '0' && *strategy <= '9'))
		return (ADAPTIVE);
	return (ERROR);
}

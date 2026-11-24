/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_init_stack_part1.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 14:21:46 by soarai            #+#    #+#             */
/*   Updated: 2026/05/28 10:56:15 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	**malloc_stack(char **argv, t_stack **stack)
{
	ssize_t	size;
	long	*memories;

	size = measure_stack(argv);
	if (size == -1 || size == 0)
	{
		free(stack);
		return (NULL);
	}
	memories = (long *)malloc(sizeof(long) * size);
	if (memories == NULL)
	{
		free(stack);
		return (NULL);
	}
	if (make_stack(argv, stack, size, memories) == NULL)
	{
		free(stack);
		stack = NULL;
	}
	free(memories);
	return (stack);
}

ssize_t	measure_stack(char **argv)
{
	ssize_t	i;
	ssize_t	start;

	i = 0;
	start = pos_dig_s(argv[1]);
	while (argv[start + i] != NULL)
	{
		if (check_digit(argv[start + i]))
			i++;
		else
			return (ERROR);
	}
	return (i);
}

ssize_t	pos_dig_s(char *target)
{
	ssize_t	start;

	start = 0;
	if (hyphen_or_digit(target))
		start = 1;
	else
		start = 2;
	return (start);
}

bool	check_digit(char *strnum)
{
	if (*strnum == '-' || *strnum == '+')
		strnum++;
	if (*strnum == '\0')
		return (false);
	while (*strnum != '\0')
	{
		if (!(*strnum >= '0' && *strnum <= '9'))
			return (false);
		strnum++;
	}
	return (true);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_init_stack_part2.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 14:22:05 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 20:13:27 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	**make_stack(char **argv, t_stack **stack, ssize_t size, long *memories)
{
	ssize_t	i;
	long	num;
	ssize_t	start;
	t_stack	*new;

	i = 0;
	start = pos_dig_s(argv[1]);
	while (i < size)
	{
		num = ft_atol(argv[start + i]);
		memories[i] = num;
		if (!check_dupmem(memories, i))
			return (ft_lstclear(stack, A));
		new = ft_lstnew(num);
		if (new == NULL)
			return (ft_lstclear(stack, A));
		ft_lstadd_back(stack, new, A);
		i++;
	}
	return (stack);
}

long	ft_atol(const char *nptr)
{
	long	num;
	long	sign;

	num = 0;
	sign = 1;
	if (*nptr == '-' || *nptr == '+')
	{
		if (*nptr == '-')
			sign = -1;
		nptr++;
	}
	while (*nptr >= '0' && *nptr <= '9')
	{
		num = num * 10 + *nptr - '0';
		nptr++;
	}
	num *= sign;
	return (num);
}

bool	check_dupmem(long *memories, size_t bp)
{
	size_t	i;

	i = 0;
	if (*(memories + bp) > INT_MAX || *(memories + bp) < INT_MIN)
		return (false);
	while (i < bp)
	{
		if (*(memories + i) == *(memories + bp))
			return (false);
		i++;
	}
	return (true);
}

t_stack	**malloc_dps(void)
{
	t_stack	**stack;

	stack = (t_stack **)malloc(sizeof(t_stack *) * 2);
	if (stack == NULL)
		return (NULL);
	*(stack + A) = NULL;
	*(stack + B) = NULL;
	return (stack);
}

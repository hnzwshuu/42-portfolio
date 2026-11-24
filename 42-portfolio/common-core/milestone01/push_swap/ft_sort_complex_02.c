/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex_02.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 15:20:33 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 15:20:45 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

size_t	make_place(size_t place)
{
	size_t	num;
	size_t	i;

	i = 1;
	num = 1;
	while (i < place)
	{
		num = num * 2;
		i++;
	}
	return (num);
}

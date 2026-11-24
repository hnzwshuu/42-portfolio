/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_adaptive.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 13:47:52 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 15:28:55 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_adaptive(t_stack **stack, int *counter, long disorder)
{
	if (disorder < 2000)
		sort_simple(stack, counter);
	else if (2000 <= disorder && disorder < 5000)
		sort_medium(stack, counter);
	else if (disorder >= 5000)
		sort_complex(stack, counter);
	return ;
}

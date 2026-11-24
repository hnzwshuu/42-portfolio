/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_utils2.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/10 18:51:49 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/13 18:17:43 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_putptr_hex(uintptr_t addr, size_t *len)
{
	char		c;

	if (addr >= 16)
	{
		if (ft_putptr_hex((addr / 16), len) == -1)
			return (-1);
	}
	if (addr % 16 < 10)
		c = (char)(addr % 16) + '0';
	else
		c = (char)(addr % 16 - 10) + 'a';
	(*len)++;
	if (write(1, &c, 1) == -1)
		return (-1);
	return (1);
}

int	ft_putptr(void *ptr, size_t *len)
{
	uintptr_t	addr;

	addr = (uintptr_t)ptr;
	if (ptr == NULL)
	{
		if (write(1, "(nil)", 5) == -1)
			return (-1);
		(*len) += 5;
		return (1);
	}
	if (write(1, "0x", 2) == -1)
		return (-1);
	else
		(*len) += 2;
	if (ft_putptr_hex(addr, len) == -1)
		return (-1);
	return (1);
}

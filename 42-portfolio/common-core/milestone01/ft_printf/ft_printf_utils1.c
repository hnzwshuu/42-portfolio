/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_utils1.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/10 17:22:55 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/13 17:55:53 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putchar(int c, size_t *len)
{
	if (write(1, &c, 1) == -1)
		return (-1);
	(*len)++;
	return (1);
}

int	ft_putstr(char *s, size_t *len)
{
	size_t	i;

	if (s == NULL)
	{
		if (write(1, "(null)", 6) == -1)
			return (-1);
		(*len) += 6;
		return (1);
	}
	i = 0;
	while (s[i] != '\0')
	{
		if (write(1, &s[i], 1) == -1)
			return (-1);
		i++;
		(*len)++;
	}
	return (1);
}

int	ft_putnbr(int n, size_t *len)
{
	long	i;
	char	c;

	i = (long)n;
	if (i < 0)
	{
		if (write(1, "-", 1) == -1)
			return (-1);
		i = -i;
		(*len)++;
	}
	if (i >= 10)
	{
		if (ft_putnbr((int)(i / 10), len) == -1)
			return (-1);
	}
	c = (char)(i % 10) + '0';
	(*len)++;
	if (write(1, &c, 1) == -1)
		return (-1);
	return (1);
}

int	ft_putnbr_unsigned(unsigned int n, size_t *len)
{
	unsigned long	i;
	char			c;

	i = (unsigned long)n;
	if (i >= 10)
	{
		if (ft_putnbr_unsigned((unsigned int)(i / 10), len) == -1)
			return (-1);
	}
	c = (char)(i % 10) + '0';
	(*len)++;
	if (write(1, &c, 1) == -1)
		return (-1);
	return (1);
}

int	ft_putnbr_hex(unsigned int n, const char *format, size_t *len)
{
	char	c;

	if (n >= 16)
	{
		if (ft_putnbr_hex(n / 16, format, len) == -1)
			return (-1);
	}
	if (n % 16 < 10)
		c = (char)(n % 16) + '0';
	else
	{
		if (*format == 'x')
			c = (char)(n % 16 - 10) + 'a';
		else
			c = (char)(n % 16 - 10) + 'A';
	}
	(*len)++;
	if (write(1, &c, 1) == -1)
		return (-1);
	return (1);
}

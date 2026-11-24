/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/10 18:48:57 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/14 16:30:44 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_print_format(const char **format, va_list ap, size_t *len)
{
	if (**format == '%')
	{
		(*format)++;
		if (ft_convert_specifier(*format, ap, len) == -1)
			return (-1);
	}
	else
	{
		if (ft_putchar(**format, len) == -1)
			return (-1);
	}
	return (1);
}

int	ft_printf(const char *format, ...)
{
	va_list	ap;
	size_t	len;

	if (!format)
		return (-1);
	va_start(ap, format);
	len = 0;
	while (*format)
	{
		if (ft_print_format(&format, ap, &len) == -1)
		{
			va_end(ap);
			return (-1);
		}
		format++;
	}
	va_end(ap);
	return (len);
}

int	ft_convert_specifier(const char *format, va_list ap, size_t *len)
{
	if (*format == 'c')
		return (ft_putchar(va_arg(ap, int), len));
	else if (*format == 's')
		return (ft_putstr(va_arg(ap, char *), len));
	else if (*format == 'p')
		return (ft_putptr(va_arg(ap, void *), len));
	else if (*format == 'd' || *format == 'i')
		return (ft_putnbr(va_arg(ap, int), len));
	else if (*format == 'u')
		return (ft_putnbr_unsigned(va_arg(ap, unsigned int), len));
	else if (*format == 'x' || *format == 'X')
		return (ft_putnbr_hex(va_arg(ap, unsigned int), format, len));
	else if (*format == '%')
		return (ft_putchar('%', len));
	else
		return (-1);
}

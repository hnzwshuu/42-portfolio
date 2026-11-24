/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/10 16:03:30 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/13 18:04:39 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <unistd.h>
# include <stdint.h>

int		ft_printf(const char *format, ...);
int		ft_putchar(int c, size_t *len);
int		ft_putstr(char *s, size_t *len);
int		ft_putnbr(int n, size_t *len);
int		ft_putnbr_unsigned(unsigned int n, size_t *len);
int		ft_putnbr_hex(unsigned int n, const char *format, size_t *len);
int		ft_convert_specifier(const char *format, va_list ap, size_t *len);
int		ft_putptr(void *ptr, size_t *len);

#endif

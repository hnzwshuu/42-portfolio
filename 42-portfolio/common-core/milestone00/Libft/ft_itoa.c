/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 20:03:44 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/07 15:05:15 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static char	*is_zero(int n)
{
	char	*str;

	(void) n;
	str = (char *)malloc(sizeof(char) * 2);
	if (!str)
		return (NULL);
	str[0] = '0';
	str[1] = '\0';
	return (str);
}

static size_t	count_len(int n)
{
	long	cast_n;
	size_t	len;

	len = 0;
	cast_n = (long)n;
	if (cast_n < 0)
		len += 1;
	while (cast_n)
	{
		cast_n /= 10;
		len++;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	long	cast_n;
	char	*str;
	size_t	len;
	size_t	len_tmp;

	cast_n = (long)n;
	if (cast_n == 0)
		return (is_zero(n));
	len = count_len((int)cast_n);
	len_tmp = len;
	if (cast_n < 0)
		cast_n = -cast_n;
	str = (char *)malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	while (cast_n)
	{
		str[len - 1] = (cast_n % 10) + '0';
		cast_n /= 10;
		len--;
	}
	if (str != (str + len))
		str[0] = '-';
	str[len_tmp] = '\0';
	return (str);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 16:12:02 by shanazaw          #+#    #+#             */
/*   Updated: 2026/04/24 14:27:03 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	unsigned char		*dst;
	const unsigned char	*src_bytes;

	if (n == 0)
		return (dest);
	dst = (unsigned char *)dest;
	src_bytes = (const unsigned char *)src;
	if (dst < src_bytes)
		return (ft_memcpy(dest, src, n));
	else
	{
		while (n > 0)
		{
			n--;
			dst[n] = src_bytes[n];
		}
	}
	return (dest);
}

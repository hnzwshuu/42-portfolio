/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 16:11:53 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/07 20:49:17 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t				i;
	unsigned char		*dst;
	const unsigned char	*src_bytes;

	i = 0;
	dst = (unsigned char *)dest;
	src_bytes = (const unsigned char *)src;
	while (i < n)
	{
		dst[i] = src_bytes[i];
		i++;
	}
	return (dest);
}

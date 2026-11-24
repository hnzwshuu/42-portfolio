/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 18:22:44 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/08 10:49:46 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	size_t			total;
	unsigned char	*a;

	if (nmemb && size && (nmemb > SIZE_MAX / size))
		return (NULL);
	total = nmemb * size;
	if (total == 0)
		total = 1;
	a = (unsigned char *)malloc(total);
	if (!a)
		return (NULL);
	ft_bzero((void *)a, total);
	return ((void *)a);
}

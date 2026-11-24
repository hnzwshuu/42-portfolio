/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 16:12:20 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/01 13:46:35 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *s, int c)
{
	char			*str;
	unsigned char	target;

	target = (unsigned char)c;
	str = (char *)s;
	while (*str)
	{
		if ((unsigned char)*str == target)
			return (str);
		str++;
	}
	if ((unsigned char)*str == target)
		return (str);
	return (0);
}

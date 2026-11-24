/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 16:13:27 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/02 17:15:45 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	char			*str;
	char			*last;
	unsigned char	target;

	str = (char *)s;
	last = 0;
	target = (unsigned char)c;
	while (*str)
	{
		if ((unsigned char)*str == target)
			last = str;
		str++;
	}
	if ((unsigned char)*str == target)
		return (str);
	return (last);
}

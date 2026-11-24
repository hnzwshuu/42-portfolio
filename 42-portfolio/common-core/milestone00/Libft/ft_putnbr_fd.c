/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 20:04:52 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/03 16:57:11 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	long	i;
	char	c;

	i = (long)n;
	if (i < 0)
	{
		write(fd, "-", 1);
		i = -i;
	}
	if (i >= 10)
		ft_putnbr_fd((int)(i / 10), fd);
	c = (char)(i % 10) + '0';
	write(fd, &c, 1);
}

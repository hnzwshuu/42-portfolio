/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libft_01.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 14:19:00 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 15:08:17 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_strlen(char *str)
{
	int	size;

	size = 0;
	while (*(str + size) != '\0')
		size++;
	return (size);
}

void	ft_putnbr_fd(int n, int fd)
{
	long	nl;
	char	asc;

	nl = (long)n;
	if (nl < 0)
	{
		nl = nl * -1;
		write(fd, "-", 1);
	}
	if (nl / 10 > 0)
		ft_putnbr_fd((int)(nl / 10), fd);
	asc = '0' + nl % 10;
	write(fd, &asc, 1);
	return ;
}

void	ft_putendl_fd(char *s, int fd)
{
	while (*s != '\0')
	{
		write(fd, s, 1);
		s++;
	}
	write(fd, "\n", 1);
	return ;
}

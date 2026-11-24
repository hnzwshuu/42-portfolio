/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   output.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:57 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	write_invalid(int code)
{
	errno = code;
	return (0);
}

int	write_all(int fd, const char *buffer, size_t length)
{
	ssize_t	written;
	int		interruptions;

	interruptions = 0;
	if (fd < 0 || (!buffer && length > 0))
		return (write_invalid(EINVAL));
	if (length > (size_t)SSIZE_MAX)
		return (write_invalid(EOVERFLOW));
	while (length > 0)
	{
		written = write(fd, buffer, length);
		if (written < 0 && errno == EINTR && interruptions++ < 8)
			continue ;
		if (written < 0)
			return (0);
		if (written == 0 || (size_t)written > length)
			return (write_invalid(EIO));
		interruptions = 0;
		buffer += written;
		length -= written;
	}
	return (1);
}

void	write_error(const char *message)
{
	if (!message)
		boundary_error("error output: null message", EINVAL);
	else if (!write_all(STDERR_FILENO, message, strlen(message)))
		boundary_error("write(stderr)", errno);
}

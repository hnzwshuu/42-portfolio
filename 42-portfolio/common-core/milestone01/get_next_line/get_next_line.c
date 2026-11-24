/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/14 12:22:15 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/18 13:30:49 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static size_t	ft_len_to_newline(char *c)
{
	size_t	i;

	i = 0;
	while (c[i] != '\n' && c[i] != '\0')
		i++;
	return (i);
}

static char	*ft_read_to_stash(int fd, char *stash)
{
	char	*buffer;
	ssize_t	bytes_read;

	while (!ft_strchr(stash, '\n'))
	{
		buffer = (char *)malloc(sizeof(char) * (BUFFER_SIZE + 1));
		if (!buffer)
			return (free(stash), NULL);
		bytes_read = read(fd, (void *)buffer, BUFFER_SIZE);
		if (bytes_read < 0)
			return (free(buffer), free(stash), NULL);
		if (bytes_read == 0)
			return (free(buffer), stash);
		buffer[bytes_read] = '\0';
		stash = ft_strjoin_free(stash, buffer);
		if (!stash)
			return (NULL);
	}
	return (stash);
}

static char	*ft_make_line(char *stash)
{
	char	*line;
	size_t	len_to_newline;
	size_t	i;

	len_to_newline = ft_len_to_newline(stash);
	if (stash[len_to_newline] == '\n')
		line = (char *)malloc(sizeof(char) * (len_to_newline + 2));
	else
		line = (char *)malloc(sizeof(char) * (len_to_newline + 1));
	if (!line)
		return (NULL);
	i = 0;
	while (i < len_to_newline)
	{
		line[i] = stash[i];
		i++;
	}
	if (stash[len_to_newline] == '\n')
	{
		line[i] = '\n';
		i++;
	}
	line[i] = '\0';
	return (line);
}

static char	*ft_update_stash(char *stash, char *line)
{
	char	*new_stash;
	size_t	line_len;
	size_t	stash_len;

	line_len = ft_strlen(line);
	stash_len = ft_strlen(stash);
	if (line_len >= stash_len)
	{
		free(stash);
		return (NULL);
	}
	new_stash = ft_substr(stash, (unsigned int)line_len,
			stash_len - line_len);
	if (!new_stash)
		return (NULL);
	if (new_stash[0] == '\0')
	{
		free(new_stash);
		new_stash = NULL;
	}
	return (new_stash);
}

char	*get_next_line(int fd)
{
	static char	*stash;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	if (stash == NULL)
		stash = ft_strdup("");
	if (!stash)
		return (NULL);
	stash = ft_read_to_stash(fd, stash);
	if (stash == NULL || stash[0] == '\0')
	{
		free(stash);
		stash = NULL;
		return (NULL);
	}
	line = ft_make_line(stash);
	if (!line)
	{
		free(stash);
		stash = NULL;
		return (NULL);
	}
	stash = ft_update_stash(stash, line);
	return (line);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 20:03:29 by shanazaw          #+#    #+#             */
/*   Updated: 2026/05/07 15:01:34 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void	free_all(char **array, size_t i)
{
	size_t	j;

	j = 0;
	while (j < i)
	{
		free(array[j]);
		j++;
	}
	free(array);
}

static size_t	count_words(char const *s, char c)
{
	size_t	count;

	count = 0;
	if (*s && *s != c)
		count = 1;
	while (*s)
	{
		if (*s == c)
		{
			s++;
			if (*s != c && *s != '\0')
				count++;
			s--;
		}
		s++;
	}
	return (count);
}

static size_t	count_word(char const *s, char c)
{
	size_t	count;

	count = 0;
	while (*s == c)
		s++;
	while (*s && *s != c)
	{
		count++;
		s++;
	}
	return (count);
}

static char	*dup_word(char const **s, char c)
{
	char	*str;
	size_t	i;

	while (**s == c)
		(*s)++;
	str = (char *)malloc(sizeof(char) * (count_word(*s, c) + 1));
	if (!str)
		return (NULL);
	i = 0;
	while (i < count_word(*s, c))
	{
		str[i] = *(*s + i);
		i++;
	}
	str[i] = '\0';
	*s = *s + count_word(*s, c);
	return (str);
}

char	**ft_split(char const *s, char c)
{
	char	**array;
	size_t	counted_words;
	size_t	i;

	if (s == NULL)
		return (NULL);
	counted_words = count_words(s, c);
	array = (char **)malloc(sizeof(char *) * (counted_words + 1));
	if (!array)
	{
		return (NULL);
	}
	i = 0;
	while (i < counted_words)
	{
		array[i] = dup_word(&s, c);
		if (!array[i])
		{
			free_all(array, i);
			return (NULL);
		}
		i++;
	}
	array[i] = NULL;
	return (array);
}

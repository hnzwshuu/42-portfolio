/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:06 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_number(const char *text, int *result)
{
	int	value;
	int	digit;

	if (!text || *text == '\0')
		return (0);
	value = 0;
	while (*text)
	{
		if (*text < '0' || *text > '9')
			return (0);
		digit = *text - '0';
		if (value > (INT_MAX - digit) / 10)
			return (0);
		value = value * 10 + digit;
		text++;
	}
	*result = value;
	return (1);
}

static int	input_error(void)
{
	write_error("Error: expected 8 valid arguments.\n"
		"Usage: ./codexion number_of_coders time_to_burnout "
		"time_to_compile time_to_debug time_to_refactor "
		"number_of_compiles_required dongle_cooldown fifo|edf\n");
	return (0);
}

static void	set_config(t_config *conf, int *values, char *scheduler)
{
	conf->count = values[0];
	conf->burnout = (t_time)values[1] * 1000;
	conf->compile = (t_time)values[2] * 1000;
	conf->debug = (t_time)values[3] * 1000;
	conf->refactor = (t_time)values[4] * 1000;
	conf->required = values[5];
	conf->cooldown = (t_time)values[6] * 1000;
	conf->edf = (strcmp(scheduler, "edf") == 0);
}

int	parse_config(int argc, char **argv, t_config *conf)
{
	int	values[7];
	int	i;

	if (argc != 9 || !argv || !conf)
		return (input_error());
	i = 0;
	while (i < 7)
	{
		if (!parse_number(argv[i + 1], &values[i]))
			return (input_error());
		i++;
	}
	if (values[0] == 0 || !argv[8] || (strcmp(argv[8], "fifo") != 0
			&& strcmp(argv[8], "edf") != 0))
		return (input_error());
	set_config(conf, values, argv[8]);
	return (1);
}

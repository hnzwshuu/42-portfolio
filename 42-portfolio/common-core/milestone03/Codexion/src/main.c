/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:53 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	cleanup(t_sim *sim, int failed)
{
	report_error(sim);
	if (!sim_destroy(sim))
	{
		report_error(sim);
		failed = 1;
		if (!sim_destroy(sim))
			return (1);
	}
	free(sim);
	return (failed);
}

int	main(int argc, char **argv)
{
	t_config	conf;
	t_sim		*sim;

	if (!parse_config(argc, argv, &conf))
		return (1);
	if (conf.required == 0)
		return (0);
	sim = malloc(sizeof(*sim));
	if (!sim)
	{
		boundary_error("malloc(sim)", errno);
		return (1);
	}
	memset(sim, 0, sizeof(*sim));
	if (!sim_init(sim, &conf))
		return (cleanup(sim, 1));
	return (cleanup(sim, sim_run(sim)));
}

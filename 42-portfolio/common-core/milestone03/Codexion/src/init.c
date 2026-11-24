/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:41 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_arrays(t_sim *sim)
{
	size_t	count;

	count = (size_t)sim->capacity;
	if (count > (size_t)-1 / sizeof(t_coder)
		|| count > (size_t)-1 / sizeof(t_dongle))
		return (record_error(sim, "allocation size overflow", EOVERFLOW));
	sim->coders = malloc(count * sizeof(t_coder));
	if (!sim->coders)
		return (record_error(sim, "malloc(coders)", errno));
	sim->dongles = malloc(count * sizeof(t_dongle));
	if (!sim->dongles)
		return (record_error(sim, "malloc(dongles)", errno));
	memset(sim->coders, 0, count * sizeof(t_coder));
	memset(sim->dongles, 0, count * sizeof(t_dongle));
	return (1);
}

static int	init_sync(t_sim *sim)
{
	int	code;

	code = pthread_mutex_init(&sim->lock, NULL);
	if (code)
		return (record_error(sim, "pthread_mutex_init(lock)", code));
	sim->sync_stage = 1;
	code = pthread_mutex_init(&sim->log_lock, NULL);
	if (code)
		return (record_error(sim, "pthread_mutex_init(log)", code));
	sim->sync_stage = 2;
	code = pthread_cond_init(&sim->event, NULL);
	if (code)
		return (record_error(sim, "pthread_cond_init(event)", code));
	sim->sync_stage = 3;
	code = pthread_cond_init(&sim->watch, NULL);
	if (code)
		return (record_error(sim, "pthread_cond_init(watch)", code));
	sim->sync_stage = 4;
	return (1);
}

static int	init_dongles(t_sim *sim)
{
	int	i;
	int	code;

	i = 0;
	while (i < sim->capacity)
	{
		code = pthread_mutex_init(&sim->dongles[i].mutex, NULL);
		if (code)
			return (record_error(sim, "pthread_mutex_init(dongle)", code));
		sim->initialized_dongles++;
		i++;
	}
	return (1);
}

static void	init_coders(t_sim *sim)
{
	int		i;

	i = 0;
	while (i < sim->conf.count)
	{
		sim->coders[i].sim = sim;
		sim->coders[i].id = i + 1;
		sim->coders[i].left = i;
		sim->coders[i].right = (i + 1) % sim->conf.count;
		sim->coders[i].initial_delay = initial_delay(&sim->conf, i);
		i++;
	}
}

int	sim_init(t_sim *sim, t_config *conf)
{
	t_config	copy;

	if (!sim || !config_valid(conf))
		return (boundary_error("sim_init: invalid argument", 0));
	if (sim->phase != SIM_EMPTY || sim->coders || sim->dongles
		|| sim->sync_stage || sim->created || sim->monitor_created
		|| sim->initialized_dongles || sim->capacity)
		return (boundary_error("sim_init: nonempty context", 0));
	copy = *conf;
	memset(sim, 0, sizeof(*sim));
	sim->conf = copy;
	sim->capacity = copy.count;
	if (!init_arrays(sim) || !init_sync(sim) || !init_dongles(sim))
		return (0);
	init_coders(sim);
	sim->phase = SIM_READY;
	return (1);
}

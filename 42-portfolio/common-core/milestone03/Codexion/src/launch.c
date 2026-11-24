/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   launch.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:45 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	sim_stop(t_sim *sim)
{
	int	code;

	if (!sim)
		return ;
	if (sim->sync_stage < 0 || sim->sync_stage > 4)
	{
		boundary_error("sim_stop: invalid metadata", 0);
		return ;
	}
	sim->stopped = 1;
	if (sim->sync_stage >= 3)
	{
		code = pthread_cond_broadcast(&sim->event);
		if (code)
			record_error(sim, "pthread_cond_broadcast(event)", code);
	}
	if (sim->sync_stage >= 4)
	{
		code = pthread_cond_broadcast(&sim->watch);
		if (code)
			record_error(sim, "pthread_cond_broadcast(watch)", code);
	}
}

static int	create_threads(t_sim *sim)
{
	int	i;
	int	code;

	i = 0;
	while (i < sim->capacity)
	{
		code = pthread_create(&sim->coders[i].thread, NULL, coder_main,
				&sim->coders[i]);
		if (code)
			return (record_error(sim, "pthread_create(coder)", code));
		sim->created++;
		i++;
	}
	code = pthread_create(&sim->monitor, NULL, monitor_main, sim);
	if (code)
		return (record_error(sim, "pthread_create(monitor)", code));
	sim->monitor_created = 1;
	return (1);
}

static int	start_threads(t_sim *sim)
{
	if (!sim_lock(sim))
		return (0);
	sim->phase = SIM_RUNNING;
	if (sim->conf.required == 0)
	{
		sim_stop(sim);
		sim->phase = SIM_DONE;
	}
	else if (!create_threads(sim))
		sim_stop(sim);
	else
		prepare_start(sim);
	return (sim_unlock(sim));
}

static int	finish_run(t_sim *sim, int joined)
{
	int	failed;

	if (!sim_lock(sim))
		return (1);
	if (joined && sim->created == 0 && sim->monitor_created == 0)
		sim->phase = SIM_DONE;
	failed = sim->failed || !joined;
	if (!sim_unlock(sim))
		return (1);
	return (failed);
}

int	sim_run(t_sim *sim)
{
	int	joined;

	if (!sim_valid(sim) || sim->phase != SIM_READY || sim->created
		|| sim->monitor_created || sim->ready || sim->stopped || sim->failed)
	{
		boundary_error("sim_run: invalid state", 0);
		return (1);
	}
	if (!start_threads(sim))
		return (1);
	joined = sim_join(sim);
	if (!joined)
		joined = sim_join(sim);
	return (finish_run(sim, joined));
}

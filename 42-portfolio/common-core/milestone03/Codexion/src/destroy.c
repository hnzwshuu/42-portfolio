/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   destroy.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:27 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	destroy_dongles(t_sim *sim)
{
	int	code;

	while (sim->initialized_dongles > 0)
	{
		code = pthread_mutex_destroy(&sim->dongles[
				sim->initialized_dongles - 1].mutex);
		if (code)
			return (record_error(sim, "pthread_mutex_destroy(dongle)", code));
		sim->initialized_dongles--;
	}
	return (1);
}

static const char	*destroy_name(int stage)
{
	if (stage == 4)
		return ("pthread_cond_destroy(watch)");
	if (stage == 3)
		return ("pthread_cond_destroy(event)");
	if (stage == 2)
		return ("pthread_mutex_destroy(log)");
	return ("pthread_mutex_destroy(lock)");
}

static int	destroy_primitive(t_sim *sim)
{
	int	code;

	if (sim->sync_stage == 4)
		code = pthread_cond_destroy(&sim->watch);
	else if (sim->sync_stage == 3)
		code = pthread_cond_destroy(&sim->event);
	else if (sim->sync_stage == 2)
		code = pthread_mutex_destroy(&sim->log_lock);
	else
		code = pthread_mutex_destroy(&sim->lock);
	if (code)
		return (record_error(sim, destroy_name(sim->sync_stage), code));
	sim->sync_stage--;
	return (1);
}

static int	destroy_sync(t_sim *sim)
{
	while (sim->sync_stage > 0)
	{
		if (!destroy_primitive(sim))
			return (0);
	}
	return (1);
}

int	sim_destroy(t_sim *sim)
{
	if (!sim)
		return (1);
	if (sim->phase == SIM_RUNNING || sim->created || sim->monitor_created)
		return (boundary_error("sim_destroy: threads remain", 0));
	if (sim->sync_stage < 0 || sim->sync_stage > 4 || sim->capacity < 0
		|| sim->initialized_dongles < 0
		|| sim->initialized_dongles > sim->capacity
		|| (!sim->dongles && sim->initialized_dongles > 0)
		|| sim->phase < SIM_EMPTY || sim->phase > SIM_DONE)
		return (boundary_error("sim_destroy: invalid metadata", 0));
	if (!destroy_dongles(sim) || !destroy_sync(sim))
		return (0);
	free(sim->coders);
	free(sim->dongles);
	memset(sim, 0, sizeof(*sim));
	return (1);
}

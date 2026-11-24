/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log_guard.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:48 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	state_message(t_coder *coder, const char *message, t_time at)
{
	if (strcmp(message, "is compiling") == 0)
		return (coder->state == CODER_COMPILING && at == coder->last_start);
	if (strcmp(message, "is debugging") == 0)
		return (coder->state == CODER_COMPILING);
	if (strcmp(message, "is refactoring") == 0)
		return (coder->state == CODER_DEBUGGING);
	if (strcmp(message, "has taken a dongle") == 0)
		return (coder->sim->capacity == 1 && coder->state == CODER_SINGLE);
	if (strcmp(message, "burned out") == 0)
		return (at >= coder->last_start
			&& at - coder->last_start >= coder->sim->conf.burnout);
	return (0);
}

int	log_valid(t_coder *coder, const char *message, t_time at)
{
	if (!coder_state_valid(coder))
		return (coder_error(coder, "log: invalid coder/index/state", EINVAL));
	if (coder->sim->stopped)
		return (0);
	if (!message || coder->sim->phase != SIM_RUNNING || !coder->sim->ready
		|| coder->sim->start < 0 || at < coder->sim->start)
		return (coder_error(coder,
				"log: invalid message/lifecycle/time", EINVAL));
	if (!state_message(coder, message, at))
		return (coder_error(coder, "log: invalid state transition", coder->id));
	return (1);
}

int	state_log_valid(t_coder *coder, const char *message, t_time at)
{
	if (!message || (strcmp(message, "has taken a dongle") != 0
			&& strcmp(message, "is debugging") != 0
			&& strcmp(message, "is refactoring") != 0))
		return (coder_error(coder, "state log: invalid message", EINVAL));
	return (log_valid(coder, message, at) && sim_active(coder->sim));
}

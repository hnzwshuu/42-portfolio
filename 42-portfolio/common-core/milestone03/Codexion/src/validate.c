/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validate.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:21 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	sim_valid(t_sim *sim)
{
	if (!sim || sim->capacity < 1)
		return (0);
	if (sim->capacity != sim->conf.count || !sim->coders || !sim->dongles)
		return (0);
	if (sim->sync_stage != 4
		|| sim->initialized_dongles != sim->capacity)
		return (0);
	return (sim->phase >= SIM_READY && sim->phase <= SIM_DONE);
}

int	coder_valid(t_coder *coder)
{
	t_sim	*sim;

	if (!coder || !sim_valid(coder->sim))
		return (0);
	sim = coder->sim;
	if (coder->id < 1 || coder->id > sim->capacity)
		return (0);
	if (coder != &sim->coders[coder->id - 1])
		return (0);
	return (coder->left == coder->id - 1
		&& coder->right == coder->id % sim->capacity);
}

int	coder_state_valid(t_coder *coder)
{
	if (!coder_valid(coder))
		return (0);
	if (coder->completed < 0 || coder->completed > coder->sim->conf.required
		|| coder->last_start < 0 || coder->initial_delay < 0)
		return (0);
	if ((coder->queued != 0 && coder->queued != 1)
		|| (coder->finished != 0 && coder->finished != 1)
		|| coder->state < CODER_WAITING || coder->state > CODER_SINGLE)
		return (0);
	return (!coder->finished
		|| coder->completed == coder->sim->conf.required);
}

int	coder_error(t_coder *coder, const char *message, int code)
{
	if (!coder)
		return (sim_error(NULL, message, code));
	return (sim_error(coder->sim, message, code));
}

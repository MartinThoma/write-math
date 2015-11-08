--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_flags`
--
ALTER TABLE `wm_flags`
  ADD CONSTRAINT `wm_flags_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_flags_ibfk_2` FOREIGN KEY (`raw_data_id`) REFERENCES `wm_raw_draw_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_formula`
--
ALTER TABLE `wm_formula`
  ADD CONSTRAINT `wm_formula_ibfk_1` FOREIGN KEY (`best_rendering`) REFERENCES `wm_renderings` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `wm_formula_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_formula_ibfk_5` FOREIGN KEY (`variant_of`) REFERENCES `wm_formula` (`id`) ON DELETE SET NULL ON UPDATE NO ACTION;

--
-- Constraints der Tabelle `wm_formula_in_paper`
--
ALTER TABLE `wm_formula_in_paper`
  ADD CONSTRAINT `wm_formula_in_paper_ibfk_1` FOREIGN KEY (`inserted_by`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_formula_old`
--
ALTER TABLE `wm_formula_old`
  ADD CONSTRAINT `wm_formula_old_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_formula_old_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_formula_svg_missing`
--
ALTER TABLE `wm_formula_svg_missing`
  ADD CONSTRAINT `wm_formula_svg_missing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_formula_svg_missing_ibfk_2` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_partial_answer`
--
ALTER TABLE `wm_partial_answer`
  ADD CONSTRAINT `wm_partial_answer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_partial_answer_ibfk_2` FOREIGN KEY (`recording_id`) REFERENCES `wm_raw_draw_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_partial_answer_ibfk_3` FOREIGN KEY (`symbol_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_raw_draw_data`
--
ALTER TABLE `wm_raw_draw_data`
  ADD CONSTRAINT `wm_raw_draw_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_raw_draw_data_ibfk_2` FOREIGN KEY (`accepted_formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `wm_renderings`
--
ALTER TABLE `wm_renderings`
  ADD CONSTRAINT `wm_renderings_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_renderings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_similarity`
--
ALTER TABLE `wm_similarity`
  ADD CONSTRAINT `wm_similarity_ibfk_1` FOREIGN KEY (`base_symbol`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_similarity_ibfk_2` FOREIGN KEY (`similar_symbol`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_tags2symbols`
--
ALTER TABLE `wm_tags2symbols`
  ADD CONSTRAINT `wm_tags2symbols_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `wm_tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_user_unknown_formula`
--
ALTER TABLE `wm_user_unknown_formula`
  ADD CONSTRAINT `wm_user_unknown_formula_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_user_unknown_formula_ibfk_2` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_users`
--
ALTER TABLE `wm_users`
  ADD CONSTRAINT `wm_users_ibfk_1` FOREIGN KEY (`language`) REFERENCES `wm_languages` (`language_code`);

--
-- Constraints der Tabelle `wm_worker_answers`
--
ALTER TABLE `wm_worker_answers`
  ADD CONSTRAINT `wm_worker_answers_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `wm_workers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_worker_answers_ibfk_2` FOREIGN KEY (`raw_data_id`) REFERENCES `wm_raw_draw_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_worker_answers_ibfk_3` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_workers`
--
ALTER TABLE `wm_workers`
  ADD CONSTRAINT `wm_workers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;


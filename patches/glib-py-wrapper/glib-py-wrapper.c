#include <glib.h>
#include <string.h>
#include <stdlib.h>

int
main (int    argc,
      char **argv)
{
  GRegex* regex;
  GString *cmd;
  gchar **args;
  gchar **exec;
  gchar *cfg;
  gchar *wd;
  gchar *wn;
  guint i;

#ifdef G_OS_WIN32
    args = g_win32_get_command_line ();
#else
    args = argv;
#endif

  /* Work directory. */
  wd = g_path_get_dirname (args[0]);

  /* Program name. */
  wn = g_path_get_basename (args[0]);
  wn = g_utf8_strdown (wn, -1);
  if (g_str_has_suffix (wn, ".exe"))
    wn[strlen (wn) - 4] = 0;

  /* Program configuration. */
  cfg = g_strdup_printf ("%s%s%s%s", wd, G_DIR_SEPARATOR_S, wn, ".config");
  if (!g_file_get_contents (cfg, &cfg, NULL, NULL))
    return -1;
  exec = g_strsplit_set (cfg, "\r\n", -1);
  if (exec == NULL)
    return -1;

  /* Command. */
  regex = g_regex_new ("\\${wd}", G_REGEX_CASELESS, 0, NULL);
  cmd = g_string_new (g_regex_replace_literal (regex, exec[0], -1, 0, wd, 0, NULL));
  for (i = 1; i < argc; i++)
    g_string_append_printf (cmd, " %s", args[i]);

  return system (g_string_free (cmd, FALSE));
}

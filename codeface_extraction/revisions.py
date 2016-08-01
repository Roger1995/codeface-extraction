# coding=utf-8
"""
This file provides the needed functions for the authors extraction.
"""

import csv_writer

from os.path import join as pathjoin


def __select_list_of_revisions(dbm, project):
    dbm.doExec("""
                    SELECT tag AS revision

                    FROM project p

                    # add releases
                    JOIN release_timeline t ON p.id = t.projectId

                    # filter for releases
                    WHERE p.name = '%s'
                    AND t.type = 'release'

                    ORDER BY t.id ASC

                    # LIMIT 10
               """ %
               project
               )

    list_of_authors = dbm.doFetchAll()
    return list_of_authors


def get_list_of_revisions(dbm, project, project_resdir):
    """
    Selects the list of revivsions for the given project, using the database-manager parameter.
    Afterwards, the list of revisions is written to the file 'revisions.list' in project_resdir.

    :param dbm: the database manager to use
    :param project: the project name to search
    :param project_resdir: the results directory of the current project

    :return the list of revisions
    """

    # get revisions for given project
    list_of_revisions = __select_list_of_revisions(dbm, project)

    # reduce the extracted list (if needed)
    lines = list_of_revisions

    # write lines to file
    outfile = pathjoin(project_resdir, "revisions.list")
    csv_writer.write_to_csv(outfile, lines)

    # return the list of revisions for use in other parts of system
    return [rev for (rev,) in list_of_revisions]

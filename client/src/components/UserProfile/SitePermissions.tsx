import React from 'react';
import { Table } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { HaztrakProfileSite } from 'store';

interface SitePermissionsProps {
  sites?: Record<string, HaztrakProfileSite>;
}

export function SitePermissions({ sites }: SitePermissionsProps) {
  return (
    <div>
      <h4>Site Permissions</h4>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>EPA ID</th>
            <th>e-Manifest</th>
          </tr>
        </thead>
        <tbody>
          {sites &&
            Object.values(sites).map((site) => (
              <tr key={`permissionsRow${site.handler.epaSiteId}`}>
                <td>
                  {site.handler.epaSiteId ? (
                    <Link to={`/site/${site.handler.epaSiteId}`}>{site.handler.epaSiteId}</Link>
                  ) : (
                    site.handler.epaSiteId
                  )}
                </td>
                <td>{site.permissions.eManifest}</td>
              </tr>
            ))}
        </tbody>
      </Table>
    </div>
  );
}

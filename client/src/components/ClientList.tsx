import { FC, useState } from 'react';
import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Avatar,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Box
} from '@mui/material';
import { MoreVert as MoreVertIcon } from '@mui/icons-material';
import { Client } from '../types';

interface ClientListProps {
  clients: Client[];
  onClientSelect: (client: Client) => void;
}

const ClientList: FC<ClientListProps> = ({ clients, onClientSelect }) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, client: Client) => {
    setAnchorEl(event.currentTarget);
    setSelectedClient(client);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedClient(null);
  };

  const handleClientSelect = () => {
    if (selectedClient) {
      onClientSelect(selectedClient);
      handleMenuClose();
    }
  };

  return (
    <>
      <Typography variant="h6" gutterBottom>
        Clients
      </Typography>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Client</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Progress</TableCell>
              <TableCell>Last Session</TableCell>
              <TableCell>Next Session</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {clients
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((client) => (
                <TableRow key={client.id}>
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <Avatar src={client.avatar} alt={client.name} />
                      <Box ml={2}>
                        <Typography variant="subtitle2">{client.name}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          {client.email}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={client.status}
                      color={
                        client.status === 'active'
                          ? 'success'
                          : client.status === 'inactive'
                          ? 'error'
                          : 'warning'
                      }
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <Box width="100%" mr={1}>
                        <LinearProgress
                          variant="determinate"
                          value={client.progress}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>
                      <Typography variant="body2" color="textSecondary">
                        {client.progress}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    {client.lastSession
                      ? new Date(client.lastSession).toLocaleDateString()
                      : 'N/A'}
                  </TableCell>
                  <TableCell>
                    {client.nextSession
                      ? new Date(client.nextSession).toLocaleDateString()
                      : 'N/A'}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={(e) => handleMenuClick(e, client)}
                    >
                      <MoreVertIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={clients.length}
        page={page}
        onPageChange={handleChangePage}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleClientSelect}>View Profile</MenuItem>
        <MenuItem onClick={handleMenuClose}>Message</MenuItem>
        <MenuItem onClick={handleMenuClose}>Schedule Session</MenuItem>
        <MenuItem onClick={handleMenuClose}>View Progress</MenuItem>
      </Menu>
    </>
  );
};

export default ClientList;
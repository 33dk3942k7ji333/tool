import logging
import ssl
from ftplib import FTP, FTP_TLS

logger = logging.getLogger()

FTP_DEBUG_LVL = 0
ENABLE_FTP_TLS = True


class FTPS(FTP_TLS):
    def ntransfercmd(self, cmd, rest=None):
        conn, size = FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p and isinstance(self.sock, ssl.SSLSocket):  # type: ignore
            session = self.sock.session
            conn = self.context.wrap_socket(
                conn,
                server_hostname=self.host,
                session=session,
            )
        return conn, size


def create_connect(host: str, user: str, pswd: str, use_ftps: bool = ENABLE_FTP_TLS):
    if use_ftps:
        ftps = None
        try:
            logger.info("Try to Use FTPS")
            ftps = FTPS(host)
            ftps.set_debuglevel(FTP_DEBUG_LVL)
            ftps.getwelcome()
            ftps.login(user, pswd)
            ftps.prot_p()
            ftps.voidcmd("TYPE I")
            logger.info("Create FTPS Success")
            return ftps
        except Exception as e:
            if ftps and isinstance(ftps, FTP):
                ftps.quit()
            logger.info(f"Create FTPS Failed with {e}")

    ftp = None
    try:
        logger.info("Try to Use FTP")
        ftp = FTP(host)
        ftp.set_debuglevel(FTP_DEBUG_LVL)
        ftp.getwelcome()
        ftp.login(user, pswd)
        ftp.voidcmd("TYPE I")
        logger.info("Create FPS Success")
        return ftp
    except Exception as e:
        if ftp and isinstance(ftp, FTP):
            ftp.quit()
        logger.error(f"Create FTP Failed: {e}", exc_info=True)

        raise ConnectionError(f"Failed to Create Connection to {host}")

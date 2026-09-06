# Juniper Junos Security Controls

## SSH-001 — SSH must use SSHv2

Junos configuration:

```text
system {
    services {
        ssh {
            protocol-version v2;
        }
    }
}
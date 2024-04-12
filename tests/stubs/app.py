from flask import Flask, request, jsonify
import ssl

app = Flask(__name__)

@app.route('/j_security_check', methods=['POST'])
def j_security_check():
    #print(request.data)
    return jsonify({}), 200


@app.route('/dataservice/device/system/status', methods=['GET'])
def dataservice_device_system_status():
    return jsonify({
        "data": [
            {
            "mem_used": "954024",
            "procs": "244",
            "disk_avail": "7015M",
            "disk_mount": "/",
            "board_type": "Sim",
            "vdevice-name": request.args.get('deviceId'),
            "total_cpu_count": "2",
            "mem_cached": "740972",
            "reboot_type": "Not Applicable",
            "disk_fs": "/dev/root",
            "fp_cpu_count": "1",
            "chassis-serial-number": "None",
            "min1_avg": "1.06",
            "state_description": "All daemons up",
            "personality": "vedge",
            "disk_used": "174M",
            "disk_use": "2",
            "disk_status": "enabled",
            "state": "green",
            "config_date/date-time-string": "Mon Feb 14 04:47:05 UTC 2022",
            "linux_cpu_count": "1",
            "cpu_user": "5.53",
            "testbed_mode": "1",
            "min15_avg": "1.08",
            "disk_size": "7615M",
            "cpu_idle": "91.96",
            "mem_buffers": "82140",
            "model_sku": "None",
            "cpu_system": "2.51",
            "version": "20.6.2-440",
            "min5_avg": "1.10",
            "tcpd_cpu_count": "0",
            "vdevice-host-name": "vm3",
            "mem_total": "3906816",
            "uptime": "16 days 05 hrs 08 min 45 sec",
            "vdevice-dataKey": request.args.get('deviceId'),
            "mem_free": "2129680",
            "bootloader_version": "Not applicable",
            "fips_mode": "enabled",
            "build_number": "440\n",
            "lastupdated": 1644814027189,
            "loghost_status": "disabled",
            "uptime-date": 1643413080000
            }
        ]
    }), 200

if __name__ == "__main__":
    context = ('./cert.pem', './key.pem') #Need to create a cert.pem and key.pem to run this
    app.run(debug=False, host='0.0.0.0', port=8080, ssl_context=context)

